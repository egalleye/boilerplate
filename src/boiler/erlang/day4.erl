-module(day4).
-export([day_four/0]).

print_young() ->
    io:fwrite("You are young~n", []).

print_old() ->
    io:fwrite("You are old~n", []).

print_teenager() ->
    io:fwrite("You are a teenager~n", []).

print_error() ->
    io:fwrite("ERROR: This person is not valid, setting age to 0.~n", []).

age(Age) when Age < 0 ->
    print_error();
age(Age) when Age >= 0, Age < 13 ->
    print_young();
age(Age) when Age >= 13, Age < 18 ->
    print_teenager();
age(_) ->
    print_old().

day_four() ->
    {ok, [Age]} = io:fread("enter age", "~d"), 
    io:fwrite("Age is ~w~n", [Age]),
    age(Age).
