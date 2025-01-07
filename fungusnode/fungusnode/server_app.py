"""fungusnode: A Flower / PyTorch app."""

from flwr.common import Context, ndarrays_to_parameters
from flwr.server import ServerApp, ServerAppComponents, ServerConfig
from flwr.server.strategy import FedAvg
from fungusnode.task import Net, get_weights
from .mastodon_client import MastodonClient
from .fungus_service import FungusService
import os
from dotenv import load_dotenv, dotenv_values
# loading variables from .env file
load_dotenv()


def server_fn(context: Context):
    client = MastodonClient()
    statuses = client.get_latest_statuses(os.getenv("NUTRIAL_TAG"))

    fungusService = FungusService()
    num_rounds, fraction_fit = [None, None]
    if statuses is not None:
        [num_rounds, fraction_fit] = fungusService.extract_config(statuses)

    # Read from config
    if num_rounds is None:
        print("No rounds found. Use local config-file")
        num_rounds = context.run_config["num-server-rounds"]
    else:
        print("Found rounds: {}".format(num_rounds))
    if fraction_fit is None:
        print("No fraction found. Use local config-file.")
        fraction_fit = context.run_config["fraction-fit"]
    else:
        print("Found fraction fit: {}".format(fraction_fit))

    # Initialize model parameters
    ndarrays = get_weights(Net())
    parameters = ndarrays_to_parameters(ndarrays)

    # Define strategy
    strategy = FedAvg(
        fraction_fit=fraction_fit,
        fraction_evaluate=1.0,
        min_available_clients=2,
        initial_parameters=parameters,
    )

    config = ServerConfig(num_rounds=num_rounds)

    return ServerAppComponents(strategy=strategy, config=config)


# Create ServerApp
app = ServerApp(server_fn=server_fn)
