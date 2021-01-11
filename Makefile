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

run1:
	python3 randomizer.py
	sudo p4run

worst1:
	python3 randomizer.py -r 1
	sudo p4run

random1:
	python3 randomizer.py -r 2
	sudo p4run

run2:
	python3 randomizer.py -v 1
	sudo p4run

worst2:
	python3 randomizer.py -v 1 -r 1
	sudo p4run

random2:
	python3 randomizer.py -v 1 -r 2
	sudo p4run

clean:
	$(info *** Cleaning...)
	sudo mn -c
	sudo rm -rf $(BUILD_DIR) $(PYCACHE_DIR) *pcap *log topology.db project*.json project*.p4i p4app.json

clean_all: clean
	sudo rm -rf $(RESULT_DIR)

aggregate: $(RESULT_DIR)
	sh aggregate.sh

receive: utils/receive.sh
	sh utils/receive.sh

send: utils/send.sh
	sh utils/send.sh

send2: utils/send.sh
	sh utils/send.sh 1