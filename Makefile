BUILD_DIR = build
PYCACHE_DIR = host_test/__pycache__

default:
	$(error Please specify a make target (see README.md))

p4-build: project.p4
	$(info *** Building P4 program...)
	p4c --target bmv2 \
		--arch v1model \
		--std p4-16 \
		-o $(BUILD_DIR)/project.json \
		--p4runtime-files $(BUILD_DIR)/project.p4info.txt \
		project.p4

build: p4-build

run:
	sudo p4run --config topology/p4app.json

clean:
	$(info *** Cleaning...)
	sudo mn -c
	sudo rm -rf $(BUILD_DIR) $(PYCACHE_DIR)