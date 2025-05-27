package com.datastudioasteroids.alma_paid_admin.data.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.datastudioasteroids.alma_paid_admin.data.model.Enrollment
import kotlinx.coroutines.flow.Flow

@Dao
interface EnrollmentDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertAll(list: List<Enrollment>)

    @Query("SELECT * FROM enrollments WHERE studentDni = :dni")
    fun getByStudent(dni: String): Flow<List<Enrollment>>
}
