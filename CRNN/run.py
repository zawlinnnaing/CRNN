import argparse
from crnn import CRNN
import os

CHAR_VECTOR = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-'.!?,\""


def parse_arguments():
    """
        Parse the command line arguments of the program.
    """

    parser = argparse.ArgumentParser(
        description="Train or test the CRNN model.")

    parser.add_argument(
        "--train", action="store_true", help="Define if we train the model"
    )
    parser.add_argument(
        "--test", action="store_true", help="Define if we test the model"
    )
    parser.add_argument(
        "-ttr",
        "--train_test_ratio",
        type=float,
        nargs="?",
        help="How the data will be split between training and testing",
        default=0.70,
    )
    parser.add_argument(
        "-m",
        "--model_path",
        type=str,
        nargs="?",
        help="The path where the pretrained model can be found or where the model will be saved",
        default="./save/",
    )
    parser.add_argument(
        "-ex",
        "--examples_path",
        type=str,
        nargs="?",
        help="The path to the file containing the examples (training samples)",
    )
    parser.add_argument(
        "-bs", "--batch_size", type=int, nargs="?", help="Size of a batch", default=64
    )
    parser.add_argument(
        "-it",
        "--iteration_count",
        type=int,
        nargs="?",
        help="How many iteration in training",
        default=10,
    )
    parser.add_argument(
        "-miw",
        "--max_image_width",
        type=int,
        nargs="?",
        help="Maximum width of an example before truncating",
        default=100,
    )
    parser.add_argument(
        "-r",
        "--restore",
        action="store_true",
        help="Define if we try to load a checkpoint file from the save folder",
    )
    parser.add_argument(
        "-cs",
        "--char_set_string",
        type=str,
        nargs="?",
        help="The charset string or file.",
        default=CHAR_VECTOR,
    )
    parser.add_argument(
        "--use_trdg",
        action="store_true",
        help="Generate training data on the fly with TextRecognitionDataGenerator",
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        nargs="?",
        help="Language to use with TRDG (Must be used with --use_trdg",
        default="en",
    )

    parser.add_argument("-lr", "--learning_rate",
                        type=float,
                        help="Learning Rate for Adam Optimizer",
                        default=0.0001)

    # parser.add_argument('-fcnn', '--freeze_cnn',
    #                     action='store_true', help="Freeze CNN layers")

    # parser.add_argument('-ft', '--first_time', action='store_true',
    #                     help='Is model restore for first time.')
    return parser.parse_args()


def main():
    """
        Entry point when using CRNN from the commandline
    """

    args = parse_arguments()

    if not args.train and not args.test:
        print("If we are not training, and not testing, what is the point?")

    crnn = None

    charset = ""
    if os.path.isfile(args.char_set_string):
        # if charset is file read from file.
        with open(args.char_set_string, "r") as f:
            while True:
                c = f.readline()
                charset += c.strip("\n")
                if not c:
                    charset += "\n"  # Add line break to charset at the end
                    break
    else:
        charset = args.char_set_string

    if args.train:
        crnn = CRNN(
            args.batch_size,
            args.model_path,
            args.examples_path,
            args.max_image_width,
            args.train_test_ratio,
            args.restore,
            charset,
            args.use_trdg,
            args.language,
            args.learning_rate
        )

        crnn.train(args.iteration_count)

    if args.test:
        if crnn is None:
            crnn = CRNN(
                args.batch_size,
                args.model_path,
                args.examples_path,
                args.max_image_width,
                0,
                args.restore,
                charset,
                args.use_trdg,
                args.language,
                args.learning_rate
            )

        crnn.test()


if __name__ == "__main__":
    main()
