# ===============
#  RPC COMPILING
# ===============
build:
	@python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. part1.proto

# ===============
#     PART 1
# ===============
run_cli_pares: build
	@./client_p1.py $(arg)

run_serv_pares_1: build
	@./server_p1.py $(arg)

run_serv_pares_2:
	./svc_par $(ARGS) qqcoisa

run_serv_central:
	./svc_cen $(ARGS)

run_cli_comp:
	./cln_cen $(ARGS)

# ===============
#    CLEANING
# ===============
clean:
	$(RM) **pb2** tests/out*.txt
