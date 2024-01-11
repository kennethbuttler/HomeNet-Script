import paramiko

# Define your server's details
hostname = '10.80.0.41'
port = 6262
username = 'net'
password = '23Silver$'  # Or use key-based authentication if configured

# Initialize an SSH client
ssh = paramiko.SSHClient()

# Automatically add the server's host key (this is insecure, see note below)
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to the server
    ssh.connect(hostname, port, username, password)

    # Start an interactive shell
    ssh_shell = ssh.invoke_shell()

    # Wait for the shell to initialize
    while not ssh_shell.recv_ready():
        pass

    # Switch to sudo mode by running the 'sudo -s' command
    ssh_shell.send('sudo -s\n')

    # Wait for the sudo password prompt
    while not ssh_shell.recv_ready():
        pass

    # Send the sudo password
    sudo_password = '23Silver$'
    ssh_shell.send(sudo_password + '\n')

    # Wait for the sudo command prompt
    while not ssh_shell.recv_ready():
        pass

    # Run the update command as root
    update_command = 'apt-get update && upgrade -y'
    ssh_shell.send(update_command + '\n')

    # Wait for the command to finish and capture the output
    update_output = ''
    while True:
        output = ssh_shell.recv(4096).decode()
        if not output:
            break
        update_output += output

    # Check if the update was successful or failed
    if 'Err:1' in update_output:
        print("Update failed")
    else:
        print("Update successful")

    # Close the SSH connection
    ssh.close()

except paramiko.AuthenticationException:
    print("Authentication failed")
except paramiko.SSHException as e:
    print("SSH connection failed:", str(e))
except Exception as e:
    print("An error occurred:", str(e))
