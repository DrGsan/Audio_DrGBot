import os


class VPN:
    def add_vpn_user(self, ssh_host, client_name):
        os.system(f'ssh {ssh_host} "sudo ikev2.sh --addclient {client_name}"')
        os.system(f'ssh {ssh_host} "rm {client_name}*"')

    def copy_sert(self, ssh_host, client_name):
        os.system(f'ssh {ssh_host} "sudo ikev2.sh --exportclient {client_name}"')
        os.system(f'scp {ssh_host}:/home/drg/{client_name}.mobileconfig /home/drg/')
        os.system(f'scp {ssh_host}:/home/drg/{client_name}.p12 /home/drg/')
        os.system(f'scp {ssh_host}:/home/drg/{client_name}.sswan /home/drg/')
        os.system(f'ssh {ssh_host} "rm {client_name}*"')

    def copy_other_files(self, ssh_host):
        file_folder = '/Users/drg/PycharmProjects/JuicyScore/job/TEMP/vpn/files'
        os.system(f'scp {file_folder}/Fun.jpg /home/drg/')
        os.system(f'scp {file_folder}/ikev2_config_import_{ssh_host.split("-")[1]}.cmd /home/drg/')
        os.system(f'scp {file_folder}/ReadMe.md /home/drg/')


def main():
    pass


if __name__ == '__main__':
    main()
