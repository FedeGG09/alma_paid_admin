package com.datastudioasteroids.alma_paid_admin.data.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.datastudioasteroids.alma_paid_admin.data.model.Student
import kotlinx.coroutines.flow.Flow

@Dao
interface StudentDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertAll(list: List<Student>)

    @Query("SELECT * FROM students WHERE dni = :dni")
    fun getByDni(dni: String): Flow<Student?>
}
