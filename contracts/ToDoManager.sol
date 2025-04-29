// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ToDoManager {
    struct Task {
        string content;
        bool completed;
    }

    Task[] public tasks;

    function addTask(string memory _content) public {
        tasks.push(Task(_content, false));
    }

    function markDone(uint _index) public {
        require(_index < tasks.length, "Invalid index");
        tasks[_index].completed = true;
    }

    function deleteTask(uint _index) public {
        require(_index < tasks.length, "Invalid index");
        for (uint i = _index; i < tasks.length - 1; i++) {
            tasks[i] = tasks[i + 1];
        }
        tasks.pop();
    }

    function getTaskCount() public view returns (uint) {
        return tasks.length;
    }

    function getTask(uint _index) public view returns (string memory, bool) {
        require(_index < tasks.length, "Invalid index");
        Task storage t = tasks[_index];
        return (t.content, t.completed);
    }
}
