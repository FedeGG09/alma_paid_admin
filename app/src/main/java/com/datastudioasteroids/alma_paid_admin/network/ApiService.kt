package com.datastudioasteroids.alma_paid_admin.network

import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface ApiService {
    @GET("/all?endpoint=all")
    suspend fun fetchAll(): List<StudentStatusDto>

    @POST("/status?endpoint=status")
    suspend fun updateStatus(@Body payload: Map<String, String>): Map<String, String>
}
