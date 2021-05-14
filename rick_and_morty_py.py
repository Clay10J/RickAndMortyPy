import argparse
import requests


def build_url(newArgs):
    category = newArgs['category'].lower()
    addons = f"/{category}"
    if newArgs['id'] is not None:
        for idx in range(len(newArgs['id'])):
            addons += ("/" if idx == 0 else ",") + f"{newArgs['id'][idx]}"
    else:
        newArgs.pop('category')
        newArgs.pop('id')
        isQueryStarted = False
        for query, value in newArgs.items():
            if value is None:
                continue
            addons += ("?" if not isQueryStarted else "&") + f"{query}={value}"

    return API_BASE_URL + addons


def print_formatted_data(json):
    json = json['results'] if type(json) is dict else json
    for obj in json:
        for key, value in obj.items():
            if type(value) is list or key == "url":
                continue
            print(f"{key} : {value['name'] if type(value) is dict else value}")
        print("\n")


def get_data(args):
    newArgs = vars(args)
    endpoint = build_url(newArgs)
    response = requests.get(endpoint)
    return response.json()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MAX_CHARACTER_ID = 671
    MAX_LOCATION_ID = 108
    MAX_EPISODE_ID = 41

    API_BASE_URL = "https://rickandmortyapi.com/api"

    # Character -> id: int
    #              name: str
    #              status: str (alive, dead or unknown)
    #              species: str
    #              type: str
    #              gender (female, male, genderless or unknown)
    # Location ->  id: int
    #              name: str
    #              type: str
    #              dimension: str
    # Episode ->   id: int
    #              name: str
    #              episode: str
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="subcommands", description="valid subcommands", dest="category",
                                       required=True, help="category to search")
    # "character" command parser
    parserCharacter = subparsers.add_parser("character", help="searches character category. add -h or --help for "
                                                              "further information")
    parserCharacter.add_argument("-id", "--id", nargs="+", type=int, choices=range(1, MAX_CHARACTER_ID + 1),
                                 help="id number to search. can be single value or space-separated list. must be in "
                                      "range 1 to 671", metavar='')
    parserCharacterFilters = parserCharacter.add_argument_group("filters", "also optional arguments. will not be used "
                                                                           "in search if -id,--id flag is present")
    parserCharacterFilters.add_argument("-n", "--name", type=str, help="name to search")
    parserCharacterFilters.add_argument("-st", "--status", type=str, choices=["alive", "dead", "unknown"],
                                        help="status to search")
    parserCharacterFilters.add_argument("-sp", "--species", type=str, help="species to search")
    parserCharacterFilters.add_argument("-t", "--type", type=str, help="type to search")
    parserCharacterFilters.add_argument("-g", "--gender", type=str, choices=["female", "male", "genderless", "unknown"],
                                        help="gender to search")

    # "location" command parser
    parserLocation = subparsers.add_parser("location", help="searches location category. add -h or --help for further "
                                                            "information")
    parserLocation.add_argument("-id", "--id", nargs="+", type=int, choices=range(1, MAX_LOCATION_ID + 1),
                                help="id number to search. can be single value or space-separated list. must be in "
                                     "range 1 to 108", metavar='')
    parserLocationFilters = parserLocation.add_argument_group("filters", "also optional arguments. will not be used "
                                                                         "in search if -id,--id flag is present")
    parserLocationFilters.add_argument("-n", "--name", type=str, help="name to search")
    parserLocationFilters.add_argument("-t", "--type", type=str, help="type to search")
    parserLocationFilters.add_argument("-d", "--dimension", type=str, help="dimension to search")

    # "episode" command parser
    parserEpisode = subparsers.add_parser("episode", help="searches episode category. add -h or --help for further "
                                                          "information")
    parserEpisode.add_argument("-id", "--id", nargs="+", type=int, choices=range(1, MAX_EPISODE_ID + 1),
                               help="id number to search. can be single value or space-separated list. must be in "
                                    "range 1 to 41", metavar='')
    parserEpisodeFilters = parserEpisode.add_argument_group("filters", "also optional arguments. will not be used in "
                                                                       "search if -id,--id flag is present")
    parserEpisodeFilters.add_argument("-n", "--name", type=str, help="name to search")
    parserEpisodeFilters.add_argument("-e", "--episode", type=str, help="episode to search")

    args = parser.parse_args()
    data = get_data(args)
    print_formatted_data(data)
