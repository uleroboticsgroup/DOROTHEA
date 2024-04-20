import time

from halo import Halo

from dorothea import Dorothea


class DorotheaPretty(Dorothea):
    """
    Class used to wrap Dorothea class and give nice cli interface.

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def doing_things(things_name, on_success):
        def decorator(func):
            def wrappper(*args, **kwargs):
                h = Halo(text=things_name)
                h.start()
                func(*args, **kwargs)
                h.succeed(on_success)

            return wrappper

        return decorator

    @doing_things("Building context set up", "Dorothea context setted up")
    def build_context_setup(self):
        super().build_context_setup()

    @doing_things("Creating networks", "Dorothea networks created")
    def _set_up_networks(self):
        super()._set_up_networks()

    @doing_things("Building docker images", "Dorothea docker images built")
    def _build_images(self):
        super()._build_images()

    @doing_things("Deploying containers", "Dorothea containers up and running")
    def _deploy_containers(self):
        super()._deploy_containers()

    # On exit

    @doing_things("Dumping flows to CSV", "Flows dumped to CSV")
    def dump_to_csv(self):
        super().dump_to_csv()

    @doing_things("Removing containers", "Dorothea containers cleaned")
    def _remove_containers(self):
        super()._remove_containers()

    @doing_things("Removing images", "Dorothea docker images cleaned")
    def _remove_images(self):
        super()._remove_images()

    @doing_things("Removing networks", "Dorothea networks cleaned")
    def _remove_networks(self):
        super()._remove_networks()
