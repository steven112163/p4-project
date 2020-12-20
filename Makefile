BUILD_DIR = build
PYCACHE_DIR = host_test/__pycache__
RESULT_DIR = results

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
	sudo p4run

clean:
	$(info *** Cleaning...)
	sudo mn -c
	sudo rm -rf $(BUILD_DIR) $(PYCACHE_DIR) $(RESULT_DIR) *pcap *log topology.db project.json project.p4i