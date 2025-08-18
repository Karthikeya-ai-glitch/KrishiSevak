package com.example.krishisevak.data.local.entities

import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.room.TypeConverters
import com.example.krishisevak.data.local.converters.Converters
import java.time.LocalDateTime

@Entity(tableName = "users")
@TypeConverters(Converters::class)
data class UserEntity(
    @PrimaryKey
    val id: Int,
    val name: String,
    val age: Int,
    val landArea: Double,
    val latitude: Double,
    val longitude: Double,
    val preferredLanguage: String,
    val isOnboardingComplete: Boolean = false,
    val createdAt: LocalDateTime = LocalDateTime.now(),
    val lastActive: LocalDateTime = LocalDateTime.now()
)

@Entity(tableName = "land_holdings")
@TypeConverters(Converters::class)
data class LandHoldingEntity(
    @PrimaryKey
    val id: String,
    val userId: String,
    val area: Double,
    val ownershipType: String,
    val soilType: String,
    val irrigationType: String?,
    val currentCrop: String?,
    val location: String,
    val latitude: Double?,
    val longitude: Double?
)

@Entity(tableName = "crops")
@TypeConverters(Converters::class)
data class CropEntity(
    @PrimaryKey
    val id: String,
    val userId: String,
    val cropName: String,
    val area: Double,
    val season: String,
    val plantedDate: LocalDateTime?,
    val expectedHarvestDate: LocalDateTime?,
    val status: String
)

@Entity(tableName = "user_preferences")
@TypeConverters(Converters::class)
data class UserPreferencesEntity(
    @PrimaryKey
    val userId: String,
    val priceAlerts: Boolean,
    val weatherUpdates: Boolean,
    val schemeUpdates: Boolean,
    val diseaseAlerts: Boolean,
    val irrigationReminders: Boolean,
    val pushNotifications: Boolean,
    val smsNotifications: Boolean,
    val emailNotifications: Boolean,
    val shareLocation: Boolean,
    val shareCropData: Boolean,
    val voiceNavigation: Boolean,
    val largeText: Boolean,
    val highContrast: Boolean,
    val autoBackup: Boolean,
    val offlineMode: Boolean,
    val dataSync: Boolean,
    val cacheSize: Int
)
