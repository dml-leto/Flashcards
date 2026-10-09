plugins {
    kotlin("jvm")
}

dependencies {
    implementation(project(":card-web"))
    implementation(project(":card-core"))
    implementation(project(":card-persistence"))
}

kotlin {
    jvmToolchain {
        languageVersion = JavaLanguageVersion.of(25)
        vendor = JvmVendorSpec.AMAZON
    }
}
