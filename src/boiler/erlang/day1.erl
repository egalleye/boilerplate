-module(day1).
-export([day_one/0]).


int() -> 4.
double() -> 4.4.
day_one() -> 
        {ok, [Int]} = io:fread("", "~d"),
        {ok, [Doub]} = io:fread("", "~f"),
        {ok, [Str]} = io:fread("", "~22c"),
             io:fwrite("day one~n"),
             io:fwrite("~w~n", [Doub + double()]),
             io:fwrite("~w~n", [Int + int()]),
             String = "for great good",
             io:fwrite("~p~n",[Str ++ String]).



