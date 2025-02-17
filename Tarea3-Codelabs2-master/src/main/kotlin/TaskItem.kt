import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.padding
import androidx.compose.material.Checkbox
import androidx.compose.material.Icon
import androidx.compose.material.IconButton
import androidx.compose.material.Text
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun TaskItem(
    task: Task, 
    onClose: (task: Task) -> Unit,
    modifier: Modifier = Modifier
) {
    val checkedState = remember { mutableStateOf(task.checked) }
    Row(
        modifier = modifier, verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            modifier = Modifier.weight(1f).padding(start = 16.dp),
            text = task.label
        )
        Checkbox(
            checked = checkedState.value,
            onCheckedChange = { checked ->
                checkedState.value = checked
                task.checked = checked 
            }
        )
        IconButton(onClick = { onClose(task) }) { 
            Icon(Icons.Filled.Close, contentDescription = "Close")
        }
    }
}
