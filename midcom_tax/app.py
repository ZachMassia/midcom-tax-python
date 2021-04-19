import sys

from midcom_tax.controller import Controller


def main():
    controller = Controller()
    sys.exit(controller.run_app())


if __name__ == '__main__':
    main()
