-module(fib).
-export([fib/0]).

run_fib(C, Fib, Lastfib) when C > 0 ->
    io:fwrite("~w ", [Fib]),
    run_fib(C-1, Fib+Lastfib, Fib);
run_fib(_, _, _) ->
    io:fwrite("~n", []). 


fib() ->
    io:fwrite("Starting Fib~n", []),
    {ok, [C]} = io:fread("Enter count", "~d"),
    run_fib(C, 1, 0).
