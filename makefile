# ===============
#  RPC COMPILING
# ===============
build:
	@python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. part1.proto
	@python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. part2.proto


# ===============
#     PART 1
# ===============
run_cli_pares: build
	@./client_p1.py $(arg)

run_serv_pares_1: build
	@./server_p1.py $(arg)

run_serv_pares_2:
	@./server_p1.py $(arg) qqcoisa

run_serv_central:
	@./server_p2.py $(arg)

run_cli_central:
	@./client_p2.py $(arg)

# ===============
#    CLEANING
# ===============
clean:
	$(RM) **pb2** tests/out*.txt tests/server_output*
