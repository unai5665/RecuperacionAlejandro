import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.runtime.Composable

@Composable
fun TaskList(
    listaItems: List<Task>,
    onCheckedTask: (task: Task, checked: Boolean) -> Unit, 
    onCloseTask: (task: Task) -> Unit 
) {
    LazyColumn {
        items(listaItems) { task ->
            TaskItem(
                task = task, 
                onClose = { onCloseTask(task) }, 
            )
        }
    }
}
