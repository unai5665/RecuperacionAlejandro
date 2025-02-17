import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.material.Button
import androidx.compose.material.Text
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable

@Composable
fun Screen() {
    var capitulosContador by rememberSaveable() { mutableStateOf(0) }
    Column {
        if (capitulosContador > 0) {
            val capitulosTexto = if (capitulosContador == 1) "capítulo" else "capítulos"
            Text("Te has visto ${capitulosContador} ${capitulosTexto} de One Piece")
        }
        Row {
            Button(
                onClick = {
                    capitulosContador++
                }
            ) {
                Text("Ver capítulo")
            }
            Button(
                onClick = {
                    capitulosContador = 0
                }
            ) {
                Text("Reiniciar contador")
            }
        }
    }
}
