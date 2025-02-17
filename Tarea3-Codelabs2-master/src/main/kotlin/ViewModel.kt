import androidx.compose.runtime.toMutableStateList
import androidx.lifecycle.ViewModel

private fun getWellnessTasks() = List(30) { i -> Task(i, "Task # $i") }

class EjemploViewModel : ViewModel() {
    private val _tasks = getWellnessTasks().toMutableStateList() 
    val tasks: List<Task> get() = _tasks

    fun remove(item:Task) {
        _tasks.remove(item)
    }

    fun changeTaskCheked(item: Task, checked: Boolean) {
        tasks.find { it.id == item.id }?.let { task ->
            task.checked = checked
        }
    }
}
