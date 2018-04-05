% Day 5
-module(day5).
-export([day_five/0]).


do_mathies(A, B, N, Exponent, Lastret) when N > 0, Exponent =:= 0 ->
    %io:fwrite("A = ~w~nB = ~w~nN = ~w~nExp = ~w~nLastret = ~w~n", [A, B, N, Exponent, Lastret]),
    io:fwrite("~w ", [(A+B*math:pow(2, Exponent))+Lastret]),
    do_mathies(A, B, N-1, Exponent+1, (A+B*math:pow(2, Exponent) + Lastret));
do_mathies(A, B, N, Exponent, Lastret) when N > 0 ->
    %io:fwrite("A = ~w~nB = ~w~nN = ~w~nExp = ~w~nLastret = ~w~n", [A, B, N, Exponent, Lastret]),
    io:fwrite("~w ", [(B*math:pow(2, Exponent))+Lastret]),
    do_mathies(A, B, N-1, Exponent+1, (B*math:pow(2, Exponent) + Lastret));
do_mathies(_, _, _, _, _) -> 
    io:fwrite("~n", []).

    


check_positive(Num, Iter) when Num =< 0 ->
    io:fwrite("Please enter a positive number greater than zero~n", []),
    process_input(Iter);
check_positive(_, _) -> done.

process_input(Iter) when Iter =:= 0 ->
    io:fwrite("Done!~n", []);
process_input(Iter) when Iter > 0 ->
    io:fwrite("Iter= ~w~n", [Iter]),
    {ok, [A]} = io:fread("Enter a~n", "~d"), 
    {ok, [B]} = io:fread("Enter b~n", "~d"), 
    {ok, [N]} = io:fread("Enter n~n", "~d"), 
    check_positive(N, Iter),
    process_input(Iter-1),
    do_mathies(A, B, N, 0, 0);
process_input(_) ->
    io:fwrite("Please enter a positive number~n", []),
    day_five().

day_five() ->
    io:fwrite("Day five~n", []),
    {ok, [Iter]} = io:fread("Enter Number of runs~n", "~d"), 
    process_input(Iter).


