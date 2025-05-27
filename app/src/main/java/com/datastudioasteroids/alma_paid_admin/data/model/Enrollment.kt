package com.datastudioasteroids.alma_paid_admin.data.model

import androidx.room.Entity

@Entity(
    tableName = "enrollments",
    primaryKeys = ["studentDni","courseId"]
)
data class Enrollment(
    val studentDni: String,
    val courseId: Long
)
