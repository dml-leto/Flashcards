plugins {
    kotlin("jvm")
}

dependencies {
    implementation(project(":card-api"))
}

kotlin {
    jvmToolchain {
        languageVersion = JavaLanguageVersion.of(25)
        vendor = JvmVendorSpec.AMAZON
    }
}
