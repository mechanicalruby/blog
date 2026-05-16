from livereload import Server
import build as builder

builder.generate_site()

server = Server()

server.watch(builder.input_path + "**/*", builder.generate_site)
server.watch("styles.css", builder.generate_site)
server.watch("t_footer.html", builder.generate_site)
server.watch("t_header.html", builder.generate_site)
server.watch(builder.output_path + "*.html")

server.serve(port=8000, root=builder.output_path)
