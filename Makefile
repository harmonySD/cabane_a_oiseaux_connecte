VENV = venv 
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

run: $(VENV)/bin/activate
	mkdir ./info_image_oiseaux/images
	mkdir ./info_image_oiseaux/images_test
	$(PYTHON) ./code/main.py


clean:
	rm -rf __pycache__
	rm -rf $(VENV)
	rm -rf my_venv
	rm -rf ./info_image_oiseaux/images/
	rm -rf ./info_image_oiseaux/images_test/



