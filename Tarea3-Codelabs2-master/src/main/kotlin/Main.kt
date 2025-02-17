import androidx.compose.desktop.ui.tooling.preview.Preview
import androidx.compose.foundation.layout.Column
import androidx.compose.material.MaterialTheme
import androidx.compose.material.Surface
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.BlendMode.Companion.Screen
import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application

@Composable
@Preview
fun App(viewModel: EjemploViewModel) {
    MaterialTheme {
        Surface {
            Column {
                Screen() 
                TaskList(
                    listaItems = viewModel.tasks,
                    onCheckedTask = { task, checked ->
                        viewModel.changeTaskCheked(task, checked)
                    },
                    onCloseTask = { task ->
                        viewModel.remove(task)
                    }
                )
            }
        }
    }
}

fun main() = application {
    val viewModel = EjemploViewModel() 
    Window(onCloseRequest = ::exitApplication) {
        App(viewModel) // Pasamos el ViewModel a la App
    }
}
