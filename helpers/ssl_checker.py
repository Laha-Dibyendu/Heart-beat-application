import socket
import datetime

# Method to check SSL expiry date
def get_ssl_expiry_date(hostname):
    import ssl
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            # Extract the expiry date string from the certificate
            expire_date_str = cert['notAfter']
            # Convert the expiry date string to a datetime object
            expire_date = datetime.datetime.strptime(expire_date_str, '%b %d %H:%M:%S %Y %Z')
            return expire_date
