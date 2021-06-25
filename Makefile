.PHONY: ;
.SILENT: ;               # no need for @
.ONESHELL: ;             # recipes execute in same shell
.NOTPARALLEL: ;          # wait for target to finish
.EXPORT_ALL_VARIABLES: ; # send all vars to shell

VERSION = 1.0.4
PACKAGE = ffmpeg-generator

# While console windows in Windows 10 do support VT (Virtual Terminal) / ANSI
# escape sequences in principle, support is turned OFF by default.
# Set-ItemProperty HKCU:\Console VirtualTerminalLevel -Type DWORD 1
# reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1

all: dep

dep:
	pip install twine
	pip install -r requirements.txt

setup: dep
	python setup.py sdist
	python setup.py bdist_wheel
	pip install dist/$(PACKAGE)-$(VERSION).tar.gz

uninstall:
	pip uninstall -y $(PACKAGE)

upload: setup
	twine upload dist/$(PACKAGE)-$(VERSION).tar.gz

docker-build:
	docker build -t rustlekarl/ffmpeg-generator:latest .

docker-exec:
	docker-compose up -d
	docker exec -it ffmpeg-generator_ffmpeg_1 bash
