package com.datastudioasteroids.alma_paid_admin.data.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.datastudioasteroids.alma_paid_admin.data.model.Course
import kotlinx.coroutines.flow.Flow

@Dao
interface CourseDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertAll(list: List<Course>)

    @Query("SELECT * FROM courses")
    fun getAll(): Flow<List<Course>>
}
