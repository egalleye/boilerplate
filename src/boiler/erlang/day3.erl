-module(day3).
-export([day_three/0]).


print_weird() ->
    io:fwrite("Weird~n", []).

print_notweird() ->
    io:fwrite("Not weird~n", []).

even(X) when X >= 6, X =< 20 ->
    print_weird();
even(_) ->
    print_notweird().
    

odd() ->
    print_weird().

eval_num(X) ->
    if (X rem 2) ==1 ->
        odd();
    true ->
        even(X)
    end.


day_three() ->
    {ok, [Num]} = io:fread("", "~d"),
    eval_num(Num).

