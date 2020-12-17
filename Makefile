default:
	$(error Please specify a make target (see README.md))

p4-build: project.p4
	$(info *** Building P4 program...)
	p4c --target bmv2 \
		--arch v1model \
		--std p4-16 \
		-o p4_compiled/project.json \
		--p4runtime-files p4_compiled/project.p4info.txt \
		project.p4

build: p4-build