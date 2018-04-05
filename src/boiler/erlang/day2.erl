-module(day2).
-export([day_two/0]).


hello(0) -> 
    0;
hello(Num) ->
    io:fwrite("hello, world~n"),
    hello(Num-1).

day_two() ->
    {ok, [Num]} = io:fread("", "~d"),
    hello(Num).
