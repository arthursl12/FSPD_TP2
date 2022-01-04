build:
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. hello.proto

run_serv_pares_1:
	./svc_par $(ARGS)

run_serv_pares_2:
	./svc_par $(ARGS) qqcoisa

run_cli_pares:
	./cln_par $(ARGS)

run_serv_central:
	./svc_cen $(ARGS)

run_cli_comp:
	./cln_cen $(ARGS)


clean:
	$(RM) **pb2**
