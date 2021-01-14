BUILD_DIR = build
PYCACHE_DIR = host_test/__pycache__
RESULT_DIR = results
COMMANDS_DIR = runtime_commands

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
	$(info ** Equal delay version 1)
	sh utils/run_tests.sh 4 1 0 0

worst1:
	$(info ** Worst case version 1)
	sh utils/run_tests.sh 4 1 0 1

random1:
	$(info ** Random case version 1)
	sh utils/run_tests.sh 4 5 0 2

ten1:
	$(info ** Random case version 1 with 10 switches)
	sh utils/run_tests.sh 10 10 0 2

tf1:
	$(info ** Random case version 1 with 25 switches)
	sh utils/run_tests.sh 25 10 0 2

run2:
	$(info ** Equal delay version 2)
	sh utils/run_tests.sh 4 1 1 0

worst2:
	$(info ** Worst case version 2)
	sh utils/run_tests.sh 4 1 1 1

random2:
	$(info ** Random case version 2)
	sh utils/run_tests.sh 4 5 1 2

ten2:
	$(info ** Random case version 2 with 10 switches)
	sh utils/run_tests.sh 10 10 1 2

tf2:
	$(info ** Random case version 2 with 25 switches)
	sh utils/run_tests.sh 25 10 1 2

clean:
	$(info *** Cleaning...)
	sudo mn -c
	sudo rm -rf $(BUILD_DIR) $(PYCACHE_DIR) $(COMMANDS_DIR) *pcap *log topology.db project*.json project*.p4i p4app.json

clean_all: clean
	sudo rm -rf $(RESULT_DIR)

aggregate: $(RESULT_DIR)
	$(info ** Aggregate results)
	sh utils/aggregate.sh 5

receive: utils/receive.sh
	sh utils/receive.sh &

send: utils/send.sh
	sh utils/send.sh 5 1 &
