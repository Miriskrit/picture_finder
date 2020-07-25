import socket
from finder import Finder


def open_html():
    with open('html/index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    return html


def open_css():
    with open('css/main.css', 'r', encoding='utf-8') as f:
        css = f.read()
    return css


def generate_response(request):

    URLS = {
        '/': open_html(),
        '/css/main.css': open_css(),
    }

    # API_____________________________
    def open_picture_html(links):
        with open('html/pick.html', 'r', encoding='utf-8') as f:
            html_begin = ''
            html_end = ''
            for i in range(28):
                html_begin += f.readline()
            for i in range(10):
                html_end += f.readline()
        html = html_begin
        for i in range(len(links)-1):
            html += '<img src=" '+links[i] + ' " alt="нет картинки">'
        html += html_end
        return html

    def parse_post(request):
        name = request.split('=')[1]
        F = Finder(name)
        html = open_picture_html(F.trade())
        return html

    # GET____________________________
    def generate_headers(url):
        if not url in URLS:
            return ('HTTP/1.1 404 Not found\n\n', 404)

        return('HTTP/1.1 200 OK', 200)

    def generate_content(code, url):
        if code == 404:
            return('<h1>404</h1><p>Not Found</p>')
        else:
            return(URLS[url])

    # MAIN___________________________
    def parse_request(request):
        try:
            parsed = request.split(' ')  # GET /users HTTP/1.1
            method = parsed[0]
            url = parsed[1]
            return (method, url)
        except:
            return(None, None)

    method, url = parse_request(request)

    if method == 'GET':
        if '?' in url and url[:9] == '/pictures':
            get_url = url.split("?")
            headers, code = generate_headers(get_url[0])
            body = parse_post(get_url[1])
            return (headers + body).encode()
        else:
            headers, code = generate_headers(url)
            body = generate_content(code, url)
            return (headers + body).encode()
    else:
        return('HTTP/1.1 405 Method not allowed\n\n<h1>405</h1><p>Method not allowed</p>').encode()


def run():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('localhost', 5000))
    serversocket.listen(5)
    print('\t\t\t\t<--Сервер запущен-->')
    print('\t\t\t\tАдрес: http://localhost:5000/\n')

    while True:
        client_socket, addr = serversocket.accept()
        request = client_socket.recv(1024)
        try:
            response = generate_response(request.decode('utf-8'))
            client_socket.sendall(response)
            print('<--ОК-->', addr, end=' ')
            print(request.decode('utf-8')[:4])
        except:
            print('<--ОШИБКА-->')
        client_socket.close()


if __name__ == "__main__":
    run()
