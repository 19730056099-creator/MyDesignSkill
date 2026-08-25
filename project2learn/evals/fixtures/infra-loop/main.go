package main

import (
	"bufio"
	"fmt"
	"net"
	"sync"
)

func handleConnection(connection net.Conn, values *sync.Map) {
	defer connection.Close()
	scanner := bufio.NewScanner(connection)
	for scanner.Scan() {
		command, err := ParseCommand(scanner.Text())
		if err != nil {
			fmt.Fprintf(connection, "ERROR %s\n", err)
			continue
		}
		if command.Name == "SET" {
			values.Store(command.Key, command.Value)
			fmt.Fprintln(connection, "OK")
			continue
		}
		value, found := values.Load(command.Key)
		if !found {
			fmt.Fprintln(connection, "NOT_FOUND")
			continue
		}
		fmt.Fprintf(connection, "VALUE %s\n", value)
	}
}

func main() {
	listener, err := net.Listen("tcp", ":4040")
	if err != nil {
		panic(err)
	}
	defer listener.Close()
	var values sync.Map
	for {
		connection, err := listener.Accept()
		if err != nil {
			continue
		}
		go handleConnection(connection, &values)
	}
}
