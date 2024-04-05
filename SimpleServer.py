import signal
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Define o código de resposta e os cabeçalhos da resposta
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # Define a resposta
        if self.path == '/':
            response_content = 'Servidor HTTP em execução!'
        elif self.path == '/hello':
            response_content = 'Olá, mundo!'
        elif self.path == '/time':
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            response_content = f'Hora atual: {current_time}'
        elif self.path == '/shutdown':
            response_content = 'Servidor sendo encerrado...'
            self.server.shutdown()  # Encerra o servidor
        else:
            response_content = '404 - Não encontrado'

        # Envia a resposta de volta para o cliente
        self.wfile.write(response_content.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=1086):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servidor HTTP escutando na porta {port}...')
    print('Ctrl+C para o servidor...')
    
    # Definindo um manipulador de sinal para capturar SIGINT (Ctrl+C)
    def signal_handler(sig, frame):
        print('Encerrando o servidor...')
        httpd.server_close()  # Fecha o socket do servidor
        exit(0)
    
    # Capturando o sinal SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Inicia o servidor
    httpd.serve_forever()

if __name__ == '__main__':
    run()
