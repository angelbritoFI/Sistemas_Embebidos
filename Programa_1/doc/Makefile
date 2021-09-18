#Declaración de variables
# Nombre del archivo principal escrito en LaTeX
PREFIX= "main"
SILENT= @
RUBBER= rubber
# Banderas para siempre generar el archivo con salida estándar PDF
FLAGS= --force --pdf
#Nombre del archivo
FILE= "bisa_questionnaire"

#Se llama en automático cada sección de este archivo
all:
	$(SILENT) make -s build
	$(SILENT) make -s clean
	$(SILENT) mv $(PREFIX).pdf $(FILE).pdf #Cambiar de nombre
	$(SILENT) make -s launch

#Compilar el proyecto
build:
	$(SILENT) $(RUBBER) $(FLAGS) $(PREFIX).tex

#Quitar toda la basura
clean:
	$(SILENT) $(RUBBER) --clean $(PREFIX).tex

#Abrir el archivo
launch:
	#gnome-open
	$(SILENT) xdg-open $(FILE).pdf &> /dev/null &

#Este archivo es para compilar desde sublime con Ctrl+B
