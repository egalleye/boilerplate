-module(day6).
-export([day_six/0]).

print_space(C) when C > 1 ->
    io:fwrite(" ", []),
    print_space(C-1);
print_space(_) -> done.

print_hash(X) when X >= 0 ->
    io:fwrite("#", []),
    print_hash(X-1);
print_hash(_) -> done.

start_pyramid(C, InitC) when C > 0 ->
    print_space(C),
    print_hash(InitC-C),
    io:fwrite("~n", []),
    start_pyramid(C-1, InitC);
start_pyramid(_, _) -> done.

day_six() ->
    io:fwrite("Day Six~n", []),
    {ok, [C]} = io:fread("Enter Count", "~d"),
    start_pyramid(C, C).
