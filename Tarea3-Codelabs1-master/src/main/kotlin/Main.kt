import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.spring
import androidx.compose.desktop.ui.tooling.preview.Preview
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.filled.KeyboardArrowUp
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application

@Composable
fun MainApp() {
    MaterialTheme {
        var showStartScreen = remember { mutableStateOf(true) }
        if (showStartScreen.value) {
            StartScreen(showStartScreen)
        } else {
            SecondScreen()
        }
    }
}

@Composable
fun StartScreen(showStartScreen: MutableState<Boolean>) {
    Column(modifier = Modifier.fillMaxSize(), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
        Text(
            text = "Welcome to the Basics Codelabs!",
            style = TextStyle(fontSize = 24.sp, color = Color.Black)
        )
        Button(
            onClick = { showStartScreen.value = false },
            colors = ButtonDefaults.buttonColors(backgroundColor = Color(0xFF6200EE)) // Color más vibrante para el botón
        ) {
            Text(text = "Continue", color = Color.White)
        }
    }
}

@Composable
fun SecondScreen(modifier: Modifier = Modifier) {
    val names: List<String> = List(1000) { "$it" }
    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(16.dp)
    ) {
        items(names) { name ->
            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
                ListItem(name, modifier = Modifier)
            }
        }
    }
}

@Composable
fun ListItem(texto: String, modifier: Modifier = Modifier) {
    var expand = rememberSaveable { mutableStateOf(false) }
    val expandPadding by animateDpAsState(
        targetValue = if (expand.value) 70.dp else 0.dp,
    )
    val currentPadding = expandPadding.coerceAtLeast(0.dp)

    Column(
        modifier = Modifier
            .background(Color(0xFFBBDEFB))
            .fillMaxWidth()
            .padding(15.dp)
            .animateContentSize(
                animationSpec = spring(
                    dampingRatio = Spring.DampingRatioMediumBouncy,
                    stiffness = Spring.StiffnessLow
                )
            ),
    ) {
        Text(
            text = ("Hello,").repeat(1),
            style = TextStyle(fontSize = 14.sp, color = Color.Black)
        )

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = texto,
                style = TextStyle(fontSize = 25.sp, color = Color.Black, fontWeight = FontWeight.Bold),
                modifier = Modifier.weight(1f)
            )
            IconButton(
                onClick = { expand.value = !expand.value },
                modifier = Modifier.padding(bottom = currentPadding)
            ) {
                Icon(
                    imageVector = if (expand.value) Icons.Filled.KeyboardArrowDown else Icons.Filled.KeyboardArrowUp,
                    contentDescription =
                        if (expand.value) "Mostrar menos" else "Mostrar más",
                    tint = Color.Black
                )
            }
        }
        if (expand.value) {
            Text(
                text = ("Composem ipsum color sit lazy, padding theme elit, sed do bouncy. ").repeat(4),
                style = TextStyle(fontSize = 14.sp, color = Color.Black),
                textAlign = TextAlign.Start
            )
        }
    }
}

fun main() = application {
    Window(onCloseRequest = ::exitApplication) {
        MainApp()
    }
}
