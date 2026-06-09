package com.gerfex.app.core

object GerfexMemory {

    private val queenMemory = mutableListOf<String>()
    private val notes = mutableListOf<String>()

    var status: String = "clean"

    fun addNote(note: String) {
        notes.add(note)
    }

    fun addQueenMemory(memory: String) {
        queenMemory.add(memory)
    }

    fun getNotes(): List<String> {
        return notes.toList()
    }

    fun getQueenMemory(): List<String> {
        return queenMemory.toList()
    }
}
