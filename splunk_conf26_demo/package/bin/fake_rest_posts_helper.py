import json
import logging
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import import_declare_test
from solnlib import conf_manager, log
from solnlib.modular_input import checkpointer
from splunklib import modularinput as smi

ADDON_NAME = "splunk_conf26_demo"
ENDPOINT = "https://jsonplaceholder.typicode.com/posts"
SOURCETYPE = "jsonplaceholder:posts"


def logger_for_input(input_name: str) -> logging.Logger:
    return log.Logs().get_logger(f"{ADDON_NAME.lower()}_{input_name}")


def get_data_from_api(logger: logging.Logger):
    logger.info(f"Getting data from {ENDPOINT}")
    request = Request(ENDPOINT, headers={"Accept": "application/json"})
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def validate_input(definition: smi.ValidationDefinition):
    return


def stream_events(inputs: smi.InputDefinition, event_writer: smi.EventWriter):
    for input_name, input_item in inputs.inputs.items():
        normalized_input_name = input_name.split("/")[-1]
        logger = logger_for_input(normalized_input_name)
        try:
            session_key = inputs.metadata["session_key"]
            log_level = conf_manager.get_log_level(
                logger=logger,
                session_key=session_key,
                app_name=ADDON_NAME,
                conf_name="splunk_conf26_demo_settings",
            )
            logger.setLevel(log_level)
            log.modular_input_start(logger, normalized_input_name)

            checkpoint = checkpointer.KVStoreCheckpointer(
                f"{ADDON_NAME}_checkpoints",
                session_key,
                ADDON_NAME,
            )
            # only ingest posts newer than the highest id seen on a previous run
            last_max_id = (checkpoint.get(normalized_input_name) or {}).get("last_max_id", 0)

            posts = get_data_from_api(logger)
            new_posts = [post for post in posts if post.get("id", 0) > last_max_id]

            for post in new_posts:
                event_writer.write_event(
                    smi.Event(
                        data=json.dumps(post, ensure_ascii=False, default=str),
                        index=input_item.get("index"),
                        sourcetype=SOURCETYPE,
                    )
                )

            if new_posts:
                checkpoint.update(
                    normalized_input_name,
                    {"last_max_id": max(post.get("id", 0) for post in new_posts)},
                )

            log.events_ingested(
                logger,
                input_name,
                SOURCETYPE,
                len(new_posts),
                input_item.get("index"),
            )
            log.modular_input_end(logger, normalized_input_name)
        except (HTTPError, URLError) as e:
            log.log_exception(
                logger,
                e,
                "http error",
                msg_before=f"Exception raised while fetching data from {ENDPOINT}: ",
            )
        except Exception as e:
            log.log_exception(
                logger,
                e,
                "fake_rest_posts error",
                msg_before="Exception raised while ingesting data for fake_rest_posts: ",
            )
