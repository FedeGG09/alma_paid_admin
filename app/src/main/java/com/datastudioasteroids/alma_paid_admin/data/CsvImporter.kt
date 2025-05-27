package com.datastudioasteroids.alma_paid_admin.data

import android.content.Context
import com.github.doyaaaaaken.kotlincsv.client.CsvReader
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

object CsvImporter {
    fun importAll(ctx: Context) {
        val db = AppDatabase.getDatabase(ctx)
        CoroutineScope(Dispatchers.IO).launch {
            val students = CsvReader().readAllWithHeader(ctx.assets.open("students.csv"))
                .map { Student(dni = it["dni"]!!, name = it["name"]!!) }
            db.studentDao().upsertAll(students)

            val courses = CsvReader().readAllWithHeader(ctx.assets.open("courses.csv"))
                .map {
                    Course(
                        id = it["id"]!!.toLong(),
                        title = it["title"]!!,
                        baseFee = it["baseFee"]!!.toDouble(),
                        dueDay = it["dueDay"]!!.toInt(),
                        latePctPerDay = it["latePctPerDay"]!!.toDouble()
                    )
                }
            db.courseDao().upsertAll(courses)

            val enrolls = CsvReader().readAllWithHeader(ctx.assets.open("enrollments.csv"))
                .map { Enrollment(studentDni = it["studentDni"]!!, courseId = it["courseId"]!!.toLong()) }
            db.enrollmentDao().upsertAll(enrolls)

            val invoices = CsvReader().readAllWithHeader(ctx.assets.open("invoices.csv"))
                .map {
                    Invoice(
                        id = it["id"]!!.toLong(),
                        studentDni = it["studentDni"]!!,
                        courseId = it["courseId"]!!.toLong(),
                        total = it["total"]!!.toDouble(),
                        surcharge = it["surcharge"]!!.toDouble(),
                        status = it["status"]!!,
                        paidAt = it["paidAt"]?.let(java.time.Instant::parse)?.toEpochMilli()
                    )
                }
            db.invoiceDao().upsertAll(invoices)
        }
    }
}
