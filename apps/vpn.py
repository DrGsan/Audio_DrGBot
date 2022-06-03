import os

remote_dir = '/home/drg'
local_dir = '/Users/drg/Downloads'


class VPN:
    def __init__(self, server_host):
        self.server_host = server_host

    def add_vpn_user(self, user_name):
        os.system(f'ssh {self.server_host} "sudo ikev2.sh --addclient {user_name}"')
        os.system(f'ssh {self.server_host} "rm {user_name}*"')

    def revoke_vpn_user(self, user_name):  # Не работает нужно подтверждение
        os.system(f'ssh {self.server_host} "sudo ikev2.sh --revokeclient {user_name}"')

    def delete_vpn_user(self, user_name):
        os.system(f'ssh {self.server_host} "sudo certutil -F -d sql:/etc/ipsec.d -n {user_name}"')

    def get_client_list(self):
        os.system(f'ssh {self.server_host} "sudo ikev2.sh --listclients"')

    def copy_sert(self, user_name):
        os.system(f'ssh {self.server_host} "sudo ikev2.sh --exportclient {user_name}"')
        os.system(f'scp {self.server_host}:{remote_dir}/{user_name}.mobileconfig {local_dir}')
        os.system(f'scp {self.server_host}:{remote_dir}/{user_name}.p12 {local_dir}')
        os.system(f'scp {self.server_host}:{remote_dir}/{user_name}.sswan {local_dir}')
        os.system(f'ssh {self.server_host} "rm {user_name}*"')

    def copy_other_files(self):
        os.system(f'scp files/Fun.jpg {local_dir}')
        os.system(f'scp files/ikev2_config_import_{self.server_host.split("-")[1]}.cmd {local_dir}')
        os.system(f'scp files/ReadMe.txt {local_dir}')


def main():
    pass
    # VPN('fb-fin').add_vpn_user('testtest')
    # VPN('fb-fin').revoke_vpn_user('testtest')
    # VPN('fb-fin').delete_vpn_user('testtest')
    # VPN('fb-fin').get_client_list()
    # VPN('fb-fin').copy_sert('testtest')
    # VPN('fb-fin').copy_other_files('testtest')


if __name__ == '__main__':
    main()
