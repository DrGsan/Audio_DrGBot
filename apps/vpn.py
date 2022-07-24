import os


class VPN:
    def __init__(self, server_host, remote_dir, local_dir):
        self.server_host = server_host
        self.remote_dir = remote_dir
        self.local_dir = local_dir

    def add_vpn_user(self, user_name):
        os.system(f'ssh {self.server_host} "sudo ikev2.sh --addclient {user_name}"')

    def copy_sert(self, user_name):
        os.system(f'ssh {self.server_host} "sudo ikev2.sh --addclient {user_name}"')

        os.system(f'ssh {self.server_host} "sudo ikev2.sh --exportclient {user_name}"')
        os.system(f'scp {self.server_host}:{self.remote_dir}/{user_name}.mobileconfig '
                  f'{self.local_dir}/{self.server_host}-{user_name}.mobileconfig')
        os.system(f'scp {self.server_host}:{self.remote_dir}/{user_name}.p12 '
                  f'{self.local_dir}/{self.server_host}-{user_name}.p12')
        os.system(f'scp {self.server_host}:{self.remote_dir}/{user_name}.sswan '
                  f'{self.local_dir}/{self.server_host}-{user_name}.sswan')

    def delete_sert_files(self, user_name):
        os.system(f'ssh {self.server_host} "rm {user_name}*"')
