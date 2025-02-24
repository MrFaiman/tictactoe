from client import Client, Host

def main() -> None:
    choice = input("Do you want to host (h) or join (j) a game? ")
    if choice.lower() == 'h':
        port = int(input("Enter port to host on: "))
        host = Host(port)
        host.play()
    else:
        host_ip = input("Enter host IP: ")
        port = int(input("Enter host port: "))
        client = Client(host_ip, port, 'O')  # Client always starts as 'O'
        client.play()

if __name__ == "__main__":
    main()