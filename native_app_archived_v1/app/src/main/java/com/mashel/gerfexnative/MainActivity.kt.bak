package com.mashel.gerfexnative

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

data class ChatMessage(val speaker: String, val text: String)

object GerfexCore {
    fun think(input: String): String {
        val text = input.trim()
        return when {
            text.isEmpty() -> "اكتب أمراً يا Mashel."
            text.contains("من انت") || text.contains("من أنت") ->
                "أنا Gerfex Native Core V1. أعمل داخل التطبيق بدون Termux."
            text.contains("كوين") || text.contains("queen", ignoreCase = true) ->
                "Queen ستكون وحدة تعلم داخلية لاحقاً. الآن النواة المحلية تعمل."
            text.contains("مرحبا") || text.contains("السلام") ->
                "مرحباً Mashel، Gerfex يعمل محلياً داخل التطبيق."
            else ->
                "Gerfex Native استلم: $text"
        }
    }
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            GerfexApp()
        }
    }
}

@Composable
fun GerfexApp() {
    var input by remember { mutableStateOf("") }
    var messages by remember {
        mutableStateOf(
            listOf(ChatMessage("Gerfex", "Gerfex Native Android V1 جاهز."))
        )
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF0B0F14))
            .padding(12.dp)
    ) {
        Text("Gerfex", color = Color.White, style = MaterialTheme.typography.headlineMedium)
        Text("Native Core V1 • بدون Termux", color = Color(0xFF4ADE80))

        Spacer(Modifier.height(12.dp))

        Column(
            modifier = Modifier
                .weight(1f)
                .verticalScroll(rememberScrollState())
        ) {
            messages.forEach {
                Text(it.speaker, color = Color(0xFF60A5FA))
                Text(it.text, color = Color.White, modifier = Modifier.padding(bottom = 10.dp))
            }
        }

        Row {
            TextField(
                value = input,
                onValueChange = { input = it },
                modifier = Modifier.weight(1f),
                placeholder = { Text("اكتب رسالة...") }
            )
            Button(
                onClick = {
                    val text = input
                    if (text.isNotBlank()) {
                        messages = messages + ChatMessage("Mashel", text)
                        messages = messages + ChatMessage("Gerfex", GerfexCore.think(text))
                        input = ""
                    }
                },
                modifier = Modifier.padding(start = 8.dp)
            ) {
                Text("↑")
            }
        }
    }
}
