package main

import "testing"

func TestParseSet(t *testing.T) {
	command, err := ParseCommand("SET name Alice")
	if err != nil || command.Name != "SET" || command.Key != "name" || command.Value != "Alice" {
		t.Fatalf("unexpected command: %#v, %v", command, err)
	}
}

func TestRejectMalformed(t *testing.T) {
	if _, err := ParseCommand("GET"); err == nil {
		t.Fatal("expected malformed command to fail")
	}
}
