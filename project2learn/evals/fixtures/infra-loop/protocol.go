package main

import (
	"errors"
	"strings"
)

type Command struct {
	Name  string
	Key   string
	Value string
}

func ParseCommand(line string) (Command, error) {
	parts := strings.Fields(strings.TrimSpace(line))
	if len(parts) == 2 && strings.ToUpper(parts[0]) == "GET" {
		return Command{Name: "GET", Key: parts[1]}, nil
	}
	if len(parts) >= 3 && strings.ToUpper(parts[0]) == "SET" {
		return Command{Name: "SET", Key: parts[1], Value: strings.Join(parts[2:], " ")}, nil
	}
	return Command{}, errors.New("expected GET key or SET key value")
}
